import polars as pl


df = (
    pl.read_csv('/ifs/groups/rosenMRIGrp/kr3288/ext_human.csv', has_header=False)
    .with_columns([
        pl.when(pl.col("column_3") > -1320.375)
        .then(pl.lit("known"))
        .otherwise(pl.lit("unknown"))
        .alias("label")
    ])
)

value_counts = df["label"].value_counts()
print(value_counts)