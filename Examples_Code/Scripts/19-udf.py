# -*- coding: utf-8 -*-
"""18-UDF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1la9_bP8HyRCcQnf8zIwUSk4C4ofSorIy
"""

import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Spark').getOrCreate()

columns = ["Seqno","Name"]
data = [("1", "john jones"),
    ("2", "tracey smith"),
    ("3", "amy sanders")]

df = spark.createDataFrame(data=data,schema=columns)

df.show(truncate=False)

def convertCase(str):
    resStr=""
    arr = str.split(" ")
    for x in arr:
       resStr= resStr + x[0:1].upper() + x[1:len(x)] + " "
    return resStr

""" Converting function to UDF 
StringType() is by default hence not required """
convertUDF = udf(lambda z: convertCase(z))

from pyspark.sql.functions import col
df.select(col("Seqno"), \
    convertUDF(col("Name")).alias("Name") ) \
   .show(truncate=False)

def upperCase(str):
    return str.upper()

upperCaseUDF = udf(lambda z:upperCase(z))   

df.withColumn("Cureated Name", upperCaseUDF(col("Name"))) \
  .show(truncate=False)

""" Using UDF on SQL """
spark.udf.register("convertUDF", convertCase)
df.createOrReplaceTempView("NAME_TABLE")
spark.sql("select Seqno, convertUDF(Name) as Name from NAME_TABLE") \
     .show(truncate=False)

@udf(returnType="String") 
def upperCase(str):
    return str.upper()

df.withColumn("Cureated Name", upperCase(col("Name"))) \
.show(truncate=False)

""""" 
No guarantee Name is not null will execute first
If convertUDF(Name) like '%John%' execute first then 
you will get runtime error
"""
spark.sql("select Seqno, convertUDF(Name) as Name from NAME_TABLE " + "where Name is not null and convertUDF(Name) like '%John%'") \
     .show(truncate=False)

""" null check """

columns = ["Seqno","Name"]
data = [("1", "john jones"),
    ("2", "tracey smith"),
    ("3", "amy sanders"),
    ('4',None)]

df2 = spark.createDataFrame(data=data,schema=columns)
df2.show(truncate=False)
df2.createOrReplaceTempView("NAME_TABLE2")

spark.sql("select convertUDF(Name)from NAME_TABLE2") \
     .show(truncate=False)

spark.udf.register("_nullsafeUDF", lambda str: convertCase(str) if not str is None else "")

spark.sql("select _nullsafeUDF(Name) from NAME_TABLE2") \
     .show(truncate=False)

spark.sql("select Seqno, _nullsafeUDF(Name) as Name from NAME_TABLE2 " + \
          " where Name is not null and _nullsafeUDF(Name) like '%John%'") \
     .show(truncate=False)

