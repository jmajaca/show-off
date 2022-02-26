package hr.show.controller;

import hr.show.dto.ImageDto;
import hr.show.service.ImageService;
import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(path = "/api/image")
public class ImageController {

    private final ImageService imageService;

    @Autowired
    public ImageController(ImageService imageService) {
        this.imageService = imageService;
    }

    /**
     * Get image by image id
     * @pathExample /api/image/123e4567-e89b-12d3-a456-426614174000
     * @param imageId image identification
     * @responseExample application/json file:examples/image.json
     * @HTTP 200 If image is found
     * @HTTP 404 If no image is found
     * @HTTP 500 For all others cases
     * */
    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ImageDto> getImage(@PathVariable("id") String imageId) {
        return ResponseEntity.of(imageService.getImage(imageId));
    }

}
