package com.example.braille2text

import android.R.string
import android.content.Context
import android.os.Bundle
import android.text.TextUtils.split
import android.util.DisplayMetrics
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_history.*
import java.io.*


class History : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_history)

        val dm = DisplayMetrics()
        windowManager.defaultDisplay.getMetrics(dm)

        val width = dm.widthPixels
        val height = dm.heightPixels

        window.setLayout((width * .9).toInt(), (height * .8).toInt())
        var history = readFromFile(this)//read in history into a string array

        val listArr = history.split("\n")   //history into EOL delimited list
        val reversedList = listArr.asReversed() //reverse it so it is recent scan at top
        val num = reversedList.size
        var mostRecent = ""
        if(num>10)
        {
            for(i in 0..9)
            {
                mostRecent += reversedList[i] + "\n"
            }
        }
        else{
            for(i in 0..num-1)
            {
                mostRecent += reversedList[i] + "\n"
            }
        }


        textView.text = mostRecent

    }

    private fun readFromFile(context: Context): String {
        var ret = ""
        try {
            val inputStream: InputStream? = context.openFileInput("history.txt")
            if (inputStream != null) {
                val inputStreamReader = InputStreamReader(inputStream)
                val bufferedReader = BufferedReader(inputStreamReader)
                var receiveString: String? = ""
                val stringBuilder = StringBuilder()


                while (bufferedReader.readLine().also { receiveString = it } != null) {
                    stringBuilder.append("\n").append(receiveString)
                }
                inputStream.close()
                ret = stringBuilder.toString()
            }
        } catch (e: FileNotFoundException) {
            Log.e("login activity", "File not found: " + e.toString())
        } catch (e: IOException) {
            Log.e("login activity", "Can not read file: " + e.toString())
        }
        return ret
    }


}