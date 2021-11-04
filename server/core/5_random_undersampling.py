from os.path import join as osjoin

from pyspark.sql import SparkSession
import pyspark.sql.types as T
import pyspark.sql.functions as F

from .directory import parquet_train_classifier_dir

def dataset_stats(df):
    min_max_avg_stats = df.groupBy(IS_PLG).agg( #36mins
        F.min(COS_SIM).alias('min'), F.max(COS_SIM).alias('max'), F.mean(COS_SIM).alias('mean')
    )
    print(min_max_avg_stats.show())


IS_PLG = 'is_plagiarism'
COS_SIM = 'cosine_similarity'
spark = SparkSession.builder.appName('test_csv').getOrCreate()
schema = T.StructType([
                       T.StructField(COS_SIM, T.FloatType(), False),
                       T.StructField(IS_PLG, T.IntegerType(), False)
])


df = spark.read.parquet(osjoin(parquet_train_classifier_dir, '*'), schema=schema, header=False)
negative_count = df.filter(df[IS_PLG] == 0)
positive_count = df.filter(df[IS_PLG] == 1)
print(f'negative {negative_count.count()}')
print(f'positive {positive_count.count()}')
print('Min, mean, max of dataset before RUS:')
dataset_stats(df)


ratio = 5*positive_count / negative_count # 4.141272527715648e-06
print(ratio)
resamples = negative_count.sample(withReplacement=False, fraction=ratio, seed=14)
under_sampled_df = resamples.union(positive_count)
print('Min, mean, max of dataset after RUS:')
dataset_stats(under_sampled_df)

pandas_df = under_sampled_df.toPandas()
pandas_df.to_parquet('rus_df.parquet')