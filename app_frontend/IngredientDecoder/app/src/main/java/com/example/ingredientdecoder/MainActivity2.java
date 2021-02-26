package com.example.ingredientdecoder;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

public class MainActivity2 extends AppCompatActivity {
    private static final int PERMISSION_CODE = 1000;
    private static final int IMAGE_CAPTURE_CODE = 1001;
    private static final int PERMISSION_CODE_UP = 1002;
    private static final int IMAGE_UPLOAD_CODE = 1003;
    private boolean ok = false;
    Button button_scan, button_upload, submit;
    ImageView imageview_a;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        button_scan = findViewById(R.id.button_scan);
        button_upload = findViewById(R.id.button_upload);
        imageview_a = findViewById(R.id.imageview_a);
        submit = findViewById(R.id.submit);
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
                    RequestQueue requestQueue = Volley.newRequestQueue(MainActivity2.this);
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
                        fea.put("type","OBJECT_LOCALIZATION");
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
                                postData.put("to_search",response.getJSONArray("responses").getJSONObject(0).
                                        getJSONArray("localizedObjectAnnotations").getJSONObject(0).getString("name"));
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            requestQueue.add(sendapi(postData, "http:52.138.39.36:3000/search_byname"));
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
                System.out.println(response);
                JSONArray arr = null;
                try {
                    arr = response.getJSONArray("message");
                    List<String> name_list = new ArrayList<String>();
                    List<String> il_list = new ArrayList<String>();
                    List<String> image_list = new ArrayList<String>();
                    List<String> owner_list = new ArrayList<String>();
                    for(int i = 0; i < arr.length(); i++){
                        name_list.add(arr.getJSONObject(i).getString("item_name"));
                        il_list.add(arr.getJSONObject(i).getString("item_list"));
                        image_list.add(arr.getJSONObject(i).getString("_id"));
                        owner_list.add(arr.getJSONObject(i).getString("owner"));
                    }
                    Intent intent = new Intent(MainActivity2.this, Result2_listActivity.class);
                    intent.putExtra("name_list", name_list.toArray(new String[0]));
                    intent.putExtra("il_list", il_list.toArray(new String[0]));
                    intent.putExtra("image_list", image_list.toArray(new String[0]));
                    intent.putExtra("owner_list", owner_list.toArray(new String[0]));
                    startActivity(intent);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
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