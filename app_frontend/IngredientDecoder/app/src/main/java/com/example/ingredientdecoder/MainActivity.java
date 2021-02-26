package com.example.ingredientdecoder;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.util.SparseArray;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;


//import com.google.cloud.vision.v1.AnnotateImageRequest;
//import com.google.cloud.vision.v1.AnnotateImageResponse;
//import com.google.cloud.vision.v1.BatchAnnotateImagesResponse;
//import com.google.cloud.vision.v1.EntityAnnotation;
//import com.google.cloud.vision.v1.Feature;
//import com.google.cloud.vision.v1.Image;
//import com.google.cloud.vision.v1.ImageAnnotatorClient;
//import com.google.protobuf.ByteString;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
//import com.google.api.client.extensions.android.json.AndroidJsonFactory;
//import com.google.api.client.http.javanet.NetHttpTransport;
//import com.google.api.services.vision.v1.Vision;
//import com.google.api.services.vision.v1.Vision.Builder;

import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.File;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.lang.reflect.Array;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import android.util.Base64;


import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.List;
import java.util.Scanner;


public class MainActivity extends AppCompatActivity {
    private static final int PERMISSION_CODE = 1000;
    private static final int IMAGE_CAPTURE_CODE = 1001;
    private static final int PERMISSION_CODE_UP = 1002;
    private static final int IMAGE_UPLOAD_CODE = 1003;
    private boolean ok = false;
    Button button_scan, button_upload, submit;
    ImageView imageview_a;
    TextView testview;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        String username = getIntent().getStringExtra("input_username");
        button_scan = findViewById(R.id.button_scan);
        button_upload = findViewById(R.id.button_upload);
        imageview_a = findViewById(R.id.imageview_a);
        Log.d("myTag", imageview_a.toString());
        submit = findViewById(R.id.submit);
        testview = findViewById(R.id.testview);
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(ok == true){
                    String url = "https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDUf4mrRJoR3_XDu8YWaNGV9BXLwpKydYs";
                    BitmapDrawable drawable = (BitmapDrawable) imageview_a.getDrawable();
                    Bitmap bbb = drawable.getBitmap();
                    ByteArrayOutputStream bos = new ByteArrayOutputStream();
                    bbb.compress(Bitmap.CompressFormat.PNG,100,bos);
                    byte[] bb = bos.toByteArray();
                    String baseeee = Base64.encodeToString(bb,0);
                    RequestQueue requestQueue = Volley.newRequestQueue(MainActivity.this);
                    JSONObject postData = new JSONObject();//http:52.138.39.36:3000/compareplist
//                    requestQueue.add(sendapi(postData, "http:52.138.39.36:3000/compareplist"));
                    try {
                        JSONArray allrequest = new JSONArray();
                        JSONObject req = new JSONObject();
                        JSONObject image = new JSONObject();
                        JSONArray allfea = new JSONArray();
                        JSONObject fea = new JSONObject();
                        image.put("content", baseeee);
                        req.put("image", image);
                        fea.put("type","TEXT_DETECTION");
                        fea.put("maxResults","1");
                        allfea.put(fea);
                        req.put("features", allfea);
                        allrequest.put(req);
                        postData.put("requests",allrequest);
                        Log.d("myTag", String.valueOf(postData));

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, postData, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println(response);
                            JSONObject postData = new JSONObject();
                            try {
                                postData.put("username", username);
                                postData.put("text_d",response.getJSONArray("responses").getJSONObject(0).
                                        getJSONArray("textAnnotations").getJSONObject(0).getString("description"));
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            requestQueue.add(sendapi(postData, "http:52.138.39.36:3000/compareplist"));
                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            error.printStackTrace();
                            Log.d("myTag", "ErrorListener");
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
            Log.d("myTag", imageview_a.toString());
            ok = true;
        }

    }

    private JsonObjectRequest sendapi(JSONObject a, String url) {

        JSONObject postData = new JSONObject();
        postData = a;
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, postData, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                System.out.println(response);
                try {
                    testview.setText(response.getString("message"));
                    Intent intent = new Intent(MainActivity.this, Result1Activity.class);
                    intent.putExtra("passtoresult", response.getString("message"));
                    startActivity(intent);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                Log.d("myTag", "response");
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
                Log.d("myTag", "no resp");
            }
        });

        return jsonObjectRequest;

    }
}