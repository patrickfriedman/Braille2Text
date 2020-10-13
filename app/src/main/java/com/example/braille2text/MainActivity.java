package com.example.braille2text;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import org.opencv.android.OpenCVLoader;

public class MainActivity extends AppCompatActivity
{
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if(OpenCVLoader.initDebug()){
            Toast.makeText(this, "OpenCV successfully loaded!", Toast.LENGTH_SHORT).show();
        }else{
            Toast.makeText(this, "OpenCV cannot be loaded", Toast.LENGTH_SHORT).show();
        }

    }
}