package com.example.braille2text

import android.content.Context
import android.graphics.BitmapFactory
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import kotlinx.android.synthetic.main.activity_translation.*
import java.io.IOException
import java.io.OutputStreamWriter


class Translation : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_translation)

        getBraille()
        val trans = getTranslate()//image processing through python
        writeToFile(trans,this)
        txtPythonShow.text = trans               //this prints out the python function to translate braille

    }

    private fun getBraille()  {
        val bmImg = BitmapFactory.decodeFile("/storage/emulated/0/DCIM/Braille/test3.jpg")
        brailleImage.setImageBitmap(bmImg)
    }

    private fun getTranslate(): String {
        val python = Python.getInstance()
        val pythonFile = python.getModule("brailleProcessingLib")
        return pythonFile.callAttr("run").toString()
    }

    private fun writeToFile(data: String, context: Context) {
        try {
            val outputStreamWriter = OutputStreamWriter(context.openFileOutput("history.txt",MODE_APPEND))
            outputStreamWriter.write(data)
            outputStreamWriter.close()
        } catch (e: IOException) {
            Log.e("Exception", "File write failed: $e")
        }
    }

}


