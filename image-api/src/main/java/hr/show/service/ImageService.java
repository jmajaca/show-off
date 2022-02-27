package hr.show.service;

import hr.show.dto.ImageDto;

import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Optional;

public interface ImageService {

    void saveImage(ImageDto imageDto);

    Optional<ImageDto> getImage(String imageId);

    void saveTextCorrection(String imageId, String value);

    String writeImage(BufferedImage image, String dirPath, String fileName);

}
