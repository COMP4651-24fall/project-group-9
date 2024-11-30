package main.java.com.project;

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

public class AccuracyChecker {
    public static class AccuracyCheckerMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable> {
        private final static IntWritable ONE =  new IntWritable(1);
        private final static IntWritable ZERO = new IntWritable(0);
        
        @Override
        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] data = value.toString().split(",");
            if (data.length < 2)
                throw new IOException("Invalid Input (len<2)");
            if (data.length % 2 != 0)
                throw new IOException("Invalid Input (not even)");

            String predict, actual;
            for (int i = 0; i < data.length; i = i + 2) {
                predict = data[i];
                actual = data[i+1];
                if (predict.equals(actual))
                    context.write(ONE, ONE);
                else
                    context.write(ONE, ZERO);
            }
        }
    }
    public static class AccuracyCheckerCombiner extends Reducer<IntWritable, IntWritable, IntWritable, IntWritable> {
        private final static IntWritable OUTPUT_KEY = new IntWritable();
        private final static IntWritable OUTPUT  = new IntWritable();

        @Override
        protected void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            int count = 0;
            for (IntWritable value : values) {
                sum = sum + value.get();
                count++;
            }
            OUTPUT_KEY.set(count);
            OUTPUT.set(sum);
            context.write(OUTPUT_KEY, OUTPUT);
        }
    }
    public static class AccuracyCheckerReducer extends Reducer<Text, IntWritable, Text, DoubleWritable> {

        @Override
        protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            int count = 0;
            count = Integer.parseInt(key.toString());
            for (IntWritable value : values) {
                sum = sum + value.get();
            }
        }
    }
}
