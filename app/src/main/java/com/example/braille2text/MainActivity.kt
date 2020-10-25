package com.example.braille2text

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import org.opencv.android.OpenCVLoader
import android.widget.Toast
import android.content.Intent
import android.view.View
import android.widget.Button
import com.chaquo.python.Python

class MainActivity : AppCompatActivity() {
    private var button: Button? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        //txtPythonShow.text=getPythonHelloWorld()                      //heres the issue

        if (OpenCVLoader.initDebug()) {
            Toast.makeText(this, "OpenCV successfully loaded!", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(this, "OpenCV cannot be loaded.", Toast.LENGTH_SHORT).show()
        }
        button = findViewById<View>(R.id.button) as Button
        button!!.setOnClickListener { openCameraActivity() }
    }

    private fun getPythonHelloWorld(): String {
        val python = Python.getInstance()
        val pythonFile = python.getModule("test")
        return pythonFile.callAttr("test").toString()
    }

    private fun openCameraActivity() {
        val intent = Intent(this, CameraActivity::class.java)
        startActivity(intent)
    }
}