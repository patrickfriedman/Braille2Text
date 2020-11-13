package com.example.braille2text

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import org.opencv.android.OpenCVLoader
import android.widget.Toast
import android.content.Intent
import android.view.TextureView
import android.view.View
import android.widget.Button
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    private var button: Button? = null
    private var button2: Button? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (OpenCVLoader.initDebug()) {
            Toast.makeText(this, "OpenCV successfully loaded!", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(this, "OpenCV cannot be loaded.", Toast.LENGTH_SHORT).show()
        }
        button = findViewById<View>(R.id.button) as Button
        button!!.setOnClickListener { openCameraActivity() }

        button2 = findViewById<View>(R.id.button2) as Button
        button2!!.setOnClickListener { openTranslationActivity() }
    }

    private fun openCameraActivity() {
        val intent = Intent(this, CameraActivity::class.java)
        startActivity(intent)
    }

    private fun openTranslationActivity() {
        val intent = Intent(this, Translation::class.java)
        startActivity(intent)
    }
}