import { Component } from '@angular/core';
import { StreamIngestionService } from '../../services/stream-ingestion.service';

@Component({
  templateUrl: './streaming-container.component.html',
  providers: [StreamIngestionService],
  standalone: true,
})
export class StreamingContainer {
  streamUrl: string = 'http://localhost:5000/video/video_feed';
  videoElement: HTMLImageElement | null = null;

  constructor(private readonly streamIngestionService: StreamIngestionService) {
    streamIngestionService
      .getVideoStream()
      .subscribe((response) => console.log(response));
  }
}
