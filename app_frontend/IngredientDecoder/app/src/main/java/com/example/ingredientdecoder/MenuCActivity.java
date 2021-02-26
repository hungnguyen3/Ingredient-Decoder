package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MenuCActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu_c);
        Button plist = findViewById(R.id.plist);
        Button scan = findViewById(R.id.scan);
        Button scani = findViewById(R.id.scani);
        String username = getIntent().getStringExtra("input_username");
        TextView nametext = findViewById(R.id.welcome_s);
        nametext.setText("Welcome "+username);
        plist.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MenuCActivity.this, pListActivity.class);
                intent.putExtra("input_username", username);
                startActivity(intent);
            }
        });
        scan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MenuCActivity.this, MainActivity.class);
                intent.putExtra("input_username", username);
                startActivity(intent);
            }
        });
        scani.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MenuCActivity.this, bynameActivity.class);
                intent.putExtra("input_username", username);
                startActivity(intent);
            }
        });


    }
}