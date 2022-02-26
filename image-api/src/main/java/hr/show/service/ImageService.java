package hr.show.service;

import hr.show.dto.ImageDto;

import java.util.Optional;

public interface ImageService {

    void saveImage(ImageDto imageDto);

    Optional<ImageDto> getImage(String imageId);

}
