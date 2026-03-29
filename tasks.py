import invoke


@invoke.task
def sort(ctx, path=".", check=False):
    """Sort module imports with ruff."""
    print("  sorting imports (ruff) ...")
    args = ["ruff", "check", "--select", "I", "--fix" if not check else "", path]
    ctx.run(" ".join(filter(None, args)))


@invoke.task
def fmt(ctx, path=".", sort_=True, check=False):
    """Run code formatter with ruff."""
    print("  formatting (ruff) ...")

    if sort_:
        sort(ctx, path, check)

    args = ["ruff", "format", path]
    if check:
        args.append("--check")
    ctx.run(" ".join(args))


@invoke.task
def lint(ctx, path="csv2http"):
    """Run linter with ruff."""
    print("  linting (ruff) ...")
    ctx.run(f"ruff check {path}")


@invoke.task
def type_check(ctx, path="."):
    """Run type checker."""
    ctx.run(f"mypy {path}")


@invoke.task
def sync_ai_skills(ctx):
    """Update the local AI agent skills."""
    print("  updating AI agent skills ...")
    base_url = "https://raw.githubusercontent.com/Kilo59/ruff-sync/main/.agents/skills/ruff-sync-usage"
    files = [
        "SKILL.md",
        "references/configuration.md",
        "references/troubleshooting.md",
        "references/ci-integration.md",
    ]
    for file in files:
        ctx.run(
            f"curl -sSL {base_url}/{file} -o .agents/skills/ruff-sync-usage/{file} --create-dirs"
        )
