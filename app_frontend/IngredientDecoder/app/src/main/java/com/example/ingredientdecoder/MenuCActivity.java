package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Bundle;
import android.os.ParcelUuid;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Set;
import java.util.UUID;

public class MenuCActivity extends AppCompatActivity {
    static final UUID mUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu_c);
        Button plist = findViewById(R.id.plist);
        Button scan = findViewById(R.id.scan);
        Button scani = findViewById(R.id.scani);
        Button bluetooth= findViewById(R.id.bluetooth);
        String username = getIntent().getStringExtra("input_username");
        TextView nametext = findViewById(R.id.welcome_s);
        nametext.setText("Welcome "+username);
        System.out.println(username.getBytes());
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


        bluetooth.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                BluetoothAdapter btAdapter = BluetoothAdapter.getDefaultAdapter();
                System.out.println(btAdapter.getBondedDevices());
                BluetoothDevice btDevice = btAdapter.getRemoteDevice("20:18:11:21:21:00");
                System.out.println(btDevice.getName());
                BluetoothSocket btSocket = null;
                int c = 0;
                do{
                    try {
                        btSocket = btDevice.createRfcommSocketToServiceRecord(mUUID);
                        System.out.println(btSocket);
                        btSocket.connect();
                        System.out.println(btSocket.isConnected());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    c++;
                }
                while (!btSocket.isConnected() && c < 3);

                try {
                    OutputStream outputStream = btSocket.getOutputStream();
                    outputStream.write(username.getBytes());
                } catch (IOException e) {
                    e.printStackTrace();
                }


                try {
                    btSocket.close();
                    System.out.println(btSocket.isConnected());
                } catch (IOException e) {
                    e.printStackTrace();
                }
                nametext.setText(username + " Bluetooth sign in finished");
            }
        });



    }

}