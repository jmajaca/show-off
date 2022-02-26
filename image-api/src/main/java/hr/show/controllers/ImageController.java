package hr.show.controllers;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(method = RequestMethod.GET, path = "/image")
public class ImageController {

    @GetMapping("/{id}")
    public ResponseEntity<?> getImage(@PathVariable("id") String imageId) {
        return ResponseEntity.ok().build();
    }

}
