package com.example.braille2text

import android.os.Bundle
import android.util.DisplayMetrics
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import kotlinx.android.synthetic.main.activity_history.*

class History : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_history)

        val dm = DisplayMetrics()
        windowManager.defaultDisplay.getMetrics(dm)

        val width = dm.widthPixels
        val height = dm.heightPixels

        window.setLayout((width * .9).toInt(), (height * .8).toInt())
        textView.text = getTranslate()                      //this prints out the python function to translate braille
    }

    private fun getTranslate(): String {
        val python = Python.getInstance()
        val pythonFile = python.getModule("brailleProcessingLib")
        return pythonFile.callAttr("run").toString()
    }
}