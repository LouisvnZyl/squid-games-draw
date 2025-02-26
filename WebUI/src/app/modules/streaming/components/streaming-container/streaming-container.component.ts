import { Component } from '@angular/core';
import { StreamIngestionService } from '../../services/stream-ingestion.service';
import { Subject, switchMap, take } from 'rxjs';

@Component({
  templateUrl: './streaming-container.component.html',
  providers: [StreamIngestionService],
  standalone: true,
})
export class StreamingContainer {
  streamUrl: string = 'http://localhost:5000/video/video-feed';
  videoElement: HTMLImageElement | null = null;

  private _stopStream$ = new Subject<void>();

  constructor(private readonly streamIngestionService: StreamIngestionService) {
    streamIngestionService
      .getVideoStream()
      .subscribe((response) => console.log(response));

    this.setUpStreamStoppingObservable();
  }

  public onStopVideo(): void {
    this._stopStream$.next();
  }

  private setUpStreamStoppingObservable(): void {
    this._stopStream$
      .pipe(
        switchMap(() => {
          console.log('Stopping Stream');

          return this.streamIngestionService.stopVideoStream();
        })
      )
      .subscribe();
  }
}
