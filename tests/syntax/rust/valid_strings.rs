pub fn strings() -> () {
    let s = "foobar";
    let s = "foo\
      bar";
    let s = "foo\

      bar";

    let s = "\
      bar";

    let escapedchars = "\\;\";\r\n\t\0";
    let octalchars = "\12;\123";
    let hexchars = "\x61;\x2B;\u{F7};\u{00F7};\u{0000F7}";
    let unicodechars = "\u{F7};\u{00F7};\u{0000F7}";

    let rs0 = r"";
    let rs1 = r#""#;
    let rs2 = r##""##;
    let rs3 = r###""###;
    let rs4 = r####""####;
    let rs5 = r#####""#####;

    let rs0 = r"foo bar";
    let rs1 = r#""foo bar""#;
    let rs2 = r##"foo "# bar"##;
    let rs3 = r###"foo "## bar"###;
    let rs4 = r####"foo "### bar"####;
    let rs5 = r#####"foo "#### bar"#####;

    let rs0 = r"foo
      bar";
    let rs1 = r#""foo
      bar""#;
    let rs2 = r##"foo
      bar"##;
    let rs3 = r###"foo
      bar"###;
    let rs4 = r####"foo
      bar"####;
    let rs5 = r#####"foo
      bar"#####;
}
