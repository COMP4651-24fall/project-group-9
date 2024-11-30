package com.project;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class CalcAcc {
    
    public static class AccuracyMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private final static IntWritable zero = new IntWritable(0);
        private Text result = new Text("result");

        @Override
        protected void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            String[] parts = value.toString().split(",");
            if (parts.length >= 2) {
                String predicted;
                String actual;
                for (int i = 0; i < parts.length; i=i+2) {
                    predicted = parts[i];
                    actual = parts[i+1];
                    if (predicted.equals(actual)) {
                        context.write(result, one);
                    } else {
                        context.write(result, zero);
                    }
                }

            }
        }
    }

    public static class AccuracyReducer extends Reducer<Text, IntWritable, Text, DoubleWritable> {
        @Override
        protected void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int total = 0;
            int correct = 0;
            for (IntWritable val : values) {
                total++;
                correct += val.get();
            }
            double accuracy = (double) correct / total;
            context.write(new Text("Accuracy"), new DoubleWritable(accuracy));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "accuracy checker");
        job.setJarByClass(CalcAcc.class);
        job.setMapperClass(AccuracyMapper.class);
        //job.setCombinerClass(AccuracyReducer.class);
        job.setReducerClass(AccuracyReducer.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);
        FileSystem.get(conf).delete(new Path(args[1]), true);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
