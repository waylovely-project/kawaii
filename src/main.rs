
fn cli() -> Command<'static> {
    Command::new("kawaii")
        .about("A fictional versioning CLI")
        .subcommand_required(true)
        .arg_required_else_help(true)
        .allow_external_subcommands(true)
        .allow_invalid_utf8_for_external_subcommands(true)
        .subcommand(
            Command::new("clone")
                .about("""Build native libraries required for Waylovely and Portals.
    Mostly they are written in C/C++. They'll get installed to the 'prebuilt-deps' folder of the root directory of the Git repository!
    This behavior can be changed by changing the "deps-location" path in kawaii/cache_config.json file.
                """),
        )
        .subcommand(
            Command::new("init")
                .about("""Initialize Kawaii build files, such as the crossfiles for Meson and other kawaii things. <3
    Run this command if you have just cloned the source code files! It's required for everything ^^""")
        )
        .subcommand(
            Command::new("add")
                .about("adds things")
                .arg_required_else_help(true)
                .arg(arg!(<PATH> ... "Stuff to add").value_parser(clap::value_parser!(PathBuf))),
        )
       
}


fn main() {
    let matches = cli().get_matches();

    match matches.subcommand() {
        Some(("init", _)) => cmd_init(),

    }
}
