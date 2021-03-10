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

public class MenuCActivity extends AppCompatActivity {

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
                try {
                    bt(username);
                } catch (IOException e) {
                    e.printStackTrace();
                }


            }
        });



    }
    private OutputStream outputStream;
    private InputStream inStream;

    private void bt(String s) throws IOException {
        BluetoothAdapter blueAdapter = BluetoothAdapter.getDefaultAdapter();
        if (blueAdapter != null) {
            if (blueAdapter.isEnabled()) {
                Set<BluetoothDevice> bondedDevices = blueAdapter.getBondedDevices();
                if(bondedDevices.size() > 0) {
                    Object[] devices = (Object []) bondedDevices.toArray();
                    System.out.println(devices);
                    BluetoothDevice device = (BluetoothDevice) devices[0];
                    ParcelUuid[] uuids = device.getUuids();
                    BluetoothSocket socket = device.createRfcommSocketToServiceRecord(uuids[0].getUuid());
                    socket.connect();
                    outputStream = socket.getOutputStream();
                    inStream = socket.getInputStream();
                    outputStream.write(s.getBytes());
                    run();
                }
                Toast.makeText(MenuCActivity.this, "No appropriate paired devices",
                        Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(MenuCActivity.this, "Bluetooth is disabled",
                        Toast.LENGTH_LONG).show();
            }
        }
    }


    public void run() {
        final int BUFFER_SIZE = 1024;
        byte[] buffer = new byte[BUFFER_SIZE];
        int bytes = 0;
        int b = BUFFER_SIZE;

        while (true) {
            try {
                bytes = inStream.read(buffer, bytes, BUFFER_SIZE - bytes);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}