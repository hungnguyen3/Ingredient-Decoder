package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

public class Result1Activity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result1);
        String result = getIntent().getStringExtra("passtoresult");
        System.out.println(result);
        TextView result1 = findViewById(R.id.result1);
        if(result.length() != 0) result1.setText("Not Safe, it has "+ result);
        else result1.setText("Safe XD");
    }
}