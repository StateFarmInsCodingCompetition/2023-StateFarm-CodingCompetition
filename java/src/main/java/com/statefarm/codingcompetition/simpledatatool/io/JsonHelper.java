package com.statefarm.codingcompetition.simpledatatool.io;

import java.nio.file.Files;
import java.nio.file.Path;

import com.google.gson.Gson;

public class JsonHelper<T> {

    public static final String RESOURCE_FOLDER_PATH = "src/main/resources/";

    private static Gson gson = new Gson();

    public T[] loadJson(String fileName) {

        String filePathString = new StringBuilder(RESOURCE_FOLDER_PATH).append(fileName).toString();
        Path filePath = Path.of(filePathString);

        try {
            String jsonAsString = new String(Files.readAllBytes(filePath));

        } catch (Exception e) {
            return null;
        }
    }

    public Gson getGson() {
        return gson;
    }
}
