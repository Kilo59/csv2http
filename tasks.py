import invoke


@invoke.task()
def sort(ctx, path="."):
    """Sort module imports."""
    print("  sorting imports ...")
    ctx.run(f"isort {path} --profile black")


@invoke.task
def fmt(ctx, path=".", sort_=True):
    """Run code formatter."""
    print("  formatting ...")
    ctx.run(f"black {path}")
    if sort_:
        sort(ctx, path)


@invoke.task
def lint(ctx, path="csv2http"):
    ctx.run(f"pylint {path}")


@invoke.task
def type_check(ctx, path="."):
    ctx.run(f"mypy {path}")
