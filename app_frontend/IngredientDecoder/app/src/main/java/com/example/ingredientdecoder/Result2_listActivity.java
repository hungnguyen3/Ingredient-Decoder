package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.Arrays;

public class Result2_listActivity extends AppCompatActivity {
    private ArrayList<String> al;
    private ArrayAdapter<String> aa;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result2_list);
        String[] name_list = getIntent().getStringArrayExtra("name_list");
        String[] il_list = getIntent().getStringArrayExtra("il_list");
        String[] image_list = getIntent().getStringArrayExtra("image_list");
        String[] owner_list = getIntent().getStringArrayExtra("owner_list");

        ListView listV = findViewById(R.id.search_res);
        String[] base = name_list;
        al = new ArrayList<>(Arrays.asList(base));
        aa = new ArrayAdapter<>(this,R.layout.search_res_list, R.id.textView3, al);
        listV.setAdapter(aa);
        listV.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Intent intent = new Intent(Result2_listActivity.this, Result2Activity.class);
                intent.putExtra("namei", name_list[position]);
                intent.putExtra("ili", il_list[position]);
                intent.putExtra("imagei", image_list[position]);
                intent.putExtra("ownerii", owner_list[position]);
                startActivity(intent);
            }
        });
    }
}