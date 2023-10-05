package com.statefarm.codingcompetition.simpledatatool.io;

import java.lang.reflect.Type;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

public class JsonHelper<T> {

    public static final String RESOURCE_FOLDER_PATH = "src/main/resources/";

    private static Gson gson = new Gson();

    public List<T> loadJson(String fileName, Class<T> clazz) {

        String filePathString = new StringBuilder(RESOURCE_FOLDER_PATH).append(fileName).toString();
        Path filePath = Path.of(filePathString);

        try {
            String jsonAsString = new String(Files.readAllBytes(filePath));

            Type typeOfT = TypeToken.getParameterized(List.class, clazz).getType();

            List<T> javaModels = gson.fromJson(jsonAsString, typeOfT);

            return javaModels;

        } catch (Exception e) {
            System.out.println(e.getMessage());
            System.out.println(e.getStackTrace());

            return null;
        }
    }

    public Gson getGson() {
        return gson;
    }
}
