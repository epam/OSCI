import pyspark
import pytest


@pytest.fixture(scope='session', autouse=True)
def spark_context():
    conf = pyspark.conf.SparkConf()
    conf.setMaster('local[*]')
    sc = pyspark.SparkContext.getOrCreate(conf=conf)
    yield sc
    sc.stop()


@pytest.fixture(scope='session')
def spark_session(spark_context: pyspark.SparkContext):
    return pyspark.sql.SparkSession.builder.config('spark.sql.shuffle.partitions', spark_context.defaultParallelism) \
        .getOrCreate()
