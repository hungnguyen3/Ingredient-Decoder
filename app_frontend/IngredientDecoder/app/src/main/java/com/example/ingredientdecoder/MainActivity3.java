package com.example.ingredientdecoder;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;

public class MainActivity3 extends AppCompatActivity { // MainActivity3 basically same as MainActivity
    private static final int PERMISSION_CODE = 1000;
    private static final int IMAGE_CAPTURE_CODE = 1001;
    private static final int PERMISSION_CODE_UP = 1002;
    private static final int IMAGE_UPLOAD_CODE = 1003;
    private boolean ok = false;
    Button button_scan, button_upload, submit;
    ImageView imageview_a;
    EditText addupname, adduplist;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main3);
        button_scan = findViewById(R.id.button_scan);
        button_upload = findViewById(R.id.button_upload);
        imageview_a = findViewById(R.id.imageview_a);
        submit = findViewById(R.id.submit);
        addupname = findViewById(R.id.addupname);
        adduplist = findViewById(R.id.adduplist);
        String username = getIntent().getStringExtra("input_username");
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(ok == true && !(adduplist.getText().toString().equals("") ||adduplist.getText().toString().equals(""))){
                    BitmapDrawable drawable = (BitmapDrawable) imageview_a.getDrawable();
                    Bitmap bbb = drawable.getBitmap();
                    ByteArrayOutputStream bos = new ByteArrayOutputStream();
                    bbb.compress(Bitmap.CompressFormat.PNG,100,bos);
                    byte[] bb = bos.toByteArray();
                    String baseeee = Base64.encodeToString(bb,0);
                    RequestQueue requestQueue = Volley.newRequestQueue(MainActivity3.this);
                    JSONObject postData = new JSONObject();
                    try {
                        postData.put("item_name", addupname.getText().toString());
                        postData.put("item_list", adduplist.getText().toString());
                        postData.put("item_image", baseeee);
                        postData.put("owner", username);

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/ilist_add", postData, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println(response);
                            Toast.makeText(MainActivity3.this, "Submitted",
                                    Toast.LENGTH_LONG).show();
                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            error.printStackTrace();
                            Log.d("myTag", "no resp");
                        }
                    });
                    requestQueue.add(jsonObjectRequest);
                }
            }
        });
        button_scan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M){
                    if(checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_DENIED ||
                            checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED){
                        String[] permission = {Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE};
                        requestPermissions(permission, PERMISSION_CODE);
                    }
                    else{
                        openCamera();
                    }
                }
                else{
                    openCamera();
                }
            }
        });
        button_upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M){
                    if(checkSelfPermission(Manifest.permission.INTERNET) == PackageManager.PERMISSION_DENIED ||
                            checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED){
                        String[] permission = {Manifest.permission.INTERNET, Manifest.permission.READ_EXTERNAL_STORAGE};
                        requestPermissions(permission, PERMISSION_CODE_UP);
                    }
                    else{
                        Intent galleryIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                        startActivityForResult(galleryIntent, IMAGE_UPLOAD_CODE);
                    }
                }
                else{
                    Intent galleryIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                    startActivityForResult(galleryIntent, IMAGE_UPLOAD_CODE);
                }
            }
        });
    }

    private void openCamera() {
        Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(cameraIntent, IMAGE_CAPTURE_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode){
            case PERMISSION_CODE:{
                if(grantResults.length>0 && grantResults[0] == PackageManager.PERMISSION_GRANTED){
                    openCamera();
                }
                else{
                    Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show();
                }
            }
            case PERMISSION_CODE_UP:{
                if(grantResults.length>0 && grantResults[0] == PackageManager.PERMISSION_GRANTED && requestCode == PERMISSION_CODE_UP){
                    Intent galleryIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                    startActivityForResult(galleryIntent, IMAGE_UPLOAD_CODE);
                }
                else if(requestCode == PERMISSION_CODE_UP){
                    Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == IMAGE_CAPTURE_CODE) {
            if(resultCode == RESULT_OK){
                Bitmap photo = (Bitmap) data.getExtras().get("data");
                imageview_a.setImageBitmap(photo);
                ok = true;
            }
        }
        else if (resultCode == RESULT_OK && requestCode == IMAGE_UPLOAD_CODE && data != null) {
            imageview_a.setImageURI(data.getData());
            ok = true;
        }

    }
}