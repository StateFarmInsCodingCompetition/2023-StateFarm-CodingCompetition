package com.statefarm.codingcompetition.simpledatatool.io;

import java.lang.reflect.Type;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDate;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;
import com.google.gson.reflect.TypeToken;

public class JsonHelper<T> {

    public static final String RESOURCE_FOLDER_PATH = "src/main/resources/";

    private static Gson gson = new GsonBuilder()
            .registerTypeAdapter(LocalDate.class, new JsonDeserializer<LocalDate>() {
                @Override
                public LocalDate deserialize(JsonElement json, Type type,
                        JsonDeserializationContext jsonDeserializationContext) throws JsonParseException {

                    return LocalDate.parse(json.getAsString());
                }
            }).create();

    public List<T> loadJson(String fileName, Class<T> clazz) {

        String filePathString = new StringBuilder(RESOURCE_FOLDER_PATH).append(fileName).toString();
        Path filePath = Path.of(filePathString);

        try {
            String jsonAsString = new String(Files.readAllBytes(filePath));

            Type typeOfT = TypeToken.getParameterized(List.class, clazz).getType();

            List<T> javaModels = gson.fromJson(jsonAsString, typeOfT);

            return javaModels;

        } catch (Exception e) {
            System.err.println(e.getMessage());
            e.printStackTrace();

            return null;
        }
    }

    public Gson getGson() {
        return gson;
    }
}
