package com.example.braille2text

import android.graphics.BitmapFactory
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import kotlinx.android.synthetic.main.activity_translation.*


class Translation : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_translation)
        getBraille()                                             //image processing through python
        txtPythonShow.text = getTranslate()                      //this prints out the python function to translate braille
    }

    private fun getBraille()  {
        val bmImg = BitmapFactory.decodeFile("/storage/emulated/0/DCIM/Braille/test.jpg")
        brailleImage.setImageBitmap(bmImg)
    }

    private fun getTranslate(): String {
        val python = Python.getInstance()
        val pythonFile = python.getModule("brailleProcessingLib")
        return pythonFile.callAttr("run").toString()
    }
}