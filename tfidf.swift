type file;
type script;

app (file tf, file tf_csv) calculate_tf (script calc_tf, string dir, file doc, string topn, string minf) {
    python @calc_tf dir topn minf @tf;
}

app (file o) merger (script merge, file[] doc) {
    python_local @merge @o @filenames(doc);
}

app (file tfidf) calculate_idf (script calc, file tf, string key, string report_top) {
    python @calc report_top @tf key stdout=@tfidf;
}

app (file final) scrounge (script s, file[] i) {
    bash @s @i stdout=@final;
}

string dir = (@arg("data"));
string report_top = (@arg("topn"));
string min_freq = (@arg("minf"));

// First map stage
script calc_tf <"calculate_tf_scores.py">;
file[] all_docs <filesys_mapper; location=dir, suffix=".txt">;
file[] doc_tf ;
foreach doc,index in all_docs {
    file tf        <single_file_mapper; file=@strcat(@doc, ".tf")>;
    file tf_csv    <single_file_mapper; file=@strcat(@doc, ".tf.csv")>;
    (tf, tf_csv)  = calculate_tf (calc_tf, dir, doc, report_top, min_freq);
    doc_tf[index] = tf;
}

// First reduce stage
script merge   <"merge.py">;
file all_tf    <single_file_mapper; file=@strcat(dir, "/collection.tf")>;
(all_tf)       = merger (merge, doc_tf );

// Second map stage
file tfidf[];
script calc_idf <"calculate_idf_scores.py">;
foreach doc, index in all_docs {
    file tfidf_t <single_file_mapper; file=@strcat(@doc, ".tfidf")>;
    (tfidf_t) = calculate_idf (calc_idf, all_tf, @filename(doc), report_top);
    tfidf[index] = tfidf_t;
}

// Second and last reduce stage
script concat <"concat.sh">;
file final <single_file_mapper; file=@strcat(dir, "/collection.tfidf.csv")>;
(final) = scrounge (concat, tfidf);
