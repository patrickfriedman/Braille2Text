package com.example.braille2text

import android.content.Context
import android.graphics.BitmapFactory
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import kotlinx.android.synthetic.main.activity_translation.*


class Translation : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_translation)
        getBraille()                                             //image processing through python
        txtPythonShow.text = getTranslate()                      //this prints out the python function to translate braille
        Toast.makeText(this,"python completed", Toast.LENGTH_SHORT).show()
       // val trans = getTranslate()
        //saveData(trans)
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

    public fun saveData(trans: String){

        val insertedText = trans    //holds translated value

        val sharedPreferences = getSharedPreferences("sharedPrefs", Context.MODE_PRIVATE)   //create shared preferences. Private to only this application
        val editor = sharedPreferences.edit()
        editor.apply{
            putString("STRING_KEY",insertedText)
        }.apply()

        Toast.makeText(this,"Data Saved", Toast.LENGTH_SHORT).show()

    }


}