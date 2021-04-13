package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

public class Result1Activity extends AppCompatActivity {  // result page of scan ingredient list function

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result1);
        String result = getIntent().getStringExtra("passtoresult");
        String isres = getIntent().getStringExtra("isresult");
        System.out.println(result);
        TextView result1 = findViewById(R.id.result1);
        TextView isrtx = findViewById(R.id.isr);
        // print the result on TextView
        if(result.length() != 0) result1.setText("Not Safe, it has "+ result);
        else result1.setText("Safe XD");
        if(isres.length() != 0) isrtx.setText("But it has some general toxic substances:\n"+ isres);
        else isrtx.setText("Also it doesn't have any general toxic substance");
    }
}