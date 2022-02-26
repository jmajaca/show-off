package hr.show.repository;

import hr.show.model.TextCorrection;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TextCorrectionRepository extends JpaRepository<TextCorrection, Long> {
}
