package hr.show.service.impl;

import hr.show.dto.ImageDto;
import hr.show.exception.NoEntityException;
import hr.show.model.Image;
import hr.show.repository.ImageRepository;
import hr.show.service.ImageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class ImageServiceImpl implements ImageService {

    private final ImageRepository imageRepository;

    @Autowired
    public ImageServiceImpl(ImageRepository imageRepository) {
        this.imageRepository = imageRepository;
    }

    @Override
    public void saveImage(ImageDto imageDto) {
        // save file to file system
        String path = "mock";
        // map
        Image image = new Image();
        image.setId(imageDto.getId());
        image.setCreationTimestamp(imageDto.getCreationDate());
        image.setPath(path);
        // save to db
        imageRepository.saveAndFlush(image);
    }

    @Override
    public Optional<ImageDto> getImage(String imageId) {
        throw new NoEntityException(Image.class, imageId);
    }
}
