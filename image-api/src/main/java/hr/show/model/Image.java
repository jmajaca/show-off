package hr.show.model;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.OneToOne;
import java.time.LocalDateTime;
import java.util.List;

@Getter
@Setter
@ToString
@EqualsAndHashCode
@RequiredArgsConstructor
@Entity
public class Image {

    @Id
    @Column(name = "id", length = 36, nullable = false)
    private String id;

    @Column(name = "path", nullable = false)
    private String path;

    @Column(name = "creation_timestamp", nullable = false)
    private LocalDateTime creationTimestamp;

    @OneToMany(mappedBy="image", cascade = CascadeType.REFRESH)
    private List<ImageBox> boxes;

    @OneToOne(mappedBy="image", cascade = CascadeType.REFRESH)
    private TextCorrection textCorrection;

}
