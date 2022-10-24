#[derive(Clone)]
struct A<'a_bж, B> {
    x: &'a_bж B,
    z: &'static str,
}

trait Tr {}

async fn f(x: Result<(), ()>) -> Result<(), ()> {
    let _ = x?;
    Ok(())
}

async fn g() {
    f(Ok(())).await.unwrap()
}

pub fn main() -> () {
    println!("\x61\x62");
    let mut x: i32 = 1;
    let s: char = 's';
    let s: char = '\123';
    let x: i32 = -1_322_i32;
    let x: Box<dyn Tr> = todo!();
    let zsd: usize = 123456usize;
    let фыва_1 = "asdf";
    let abra_cadabra_2 = r#"abcd"#;
    let x = 1;
    let asd = r###"sdasd sdf"###;
    let abra_cadabra_2 = r#"multiline
        string
    "#;
    let asd = r###"multiline string
        any characters '"_\/%
        abcd"###;
    return ();
}
