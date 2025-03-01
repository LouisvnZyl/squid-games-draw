import { Component, OnDestroy } from '@angular/core';
import { StreamIngestionService } from '../../services/stream-ingestion.service';
import {
  BehaviorSubject,
  catchError,
  interval,
  Observable,
  of,
  Subject,
  switchMap,
  takeUntil,
} from 'rxjs';
import { CommonModule } from '@angular/common';
import { LoadingSpinnerComponent } from 'src/app/shared/components/loading-spinner/loading-spinner.component';
import { ButtonComponent } from 'src/app/shared/components/button/button.component';
import { ImageProcessingService } from '../../services/image-processing.service';

@Component({
  templateUrl: './streaming-container.component.html',
  styleUrls: ['./streaming-container.component.scss'],
  providers: [StreamIngestionService, ImageProcessingService],
  imports: [CommonModule, LoadingSpinnerComponent, ButtonComponent],
  standalone: true,
})
export class StreamingContainer implements OnDestroy {
  streamUrl: string = 'http://localhost:5000/video/video-feed';
  videoElement: HTMLImageElement | null = null;

  public drawnImageUrl: string | undefined = '';

  public readonly isStreamActive$ = new BehaviorSubject<boolean>(false);

  private readonly _stopStream$ = new Subject<void>();
  private readonly _startStream$ = new Subject<void>();
  private readonly _destroy$ = new Subject<void>();
  private readonly _getDrawnImage$ = new Subject<void>();

  constructor(
    private readonly streamIngestionService: StreamIngestionService,
    private readonly imageProcessingService: ImageProcessingService
  ) {
    this.setUpStreamStoppingObservable();
    this.setUpStreamEvaluation();
    this.setUpStartStream();
    this.setUpGetDrawnImage();
  }

  public ngOnDestroy(): void {
    this._destroy$.next();
    this._destroy$.complete();
  }

  public startStream(): void {
    this._startStream$.next();
  }

  public onStopVideo(): void {
    this._stopStream$.next();
  }

  private setUpStartStream(): void {
    this._startStream$
      .pipe(
        switchMap(() => this.streamIngestionService.getVideoStream()),
        takeUntil(this._destroy$)
      )
      .subscribe();
  }

  private setUpStreamEvaluation(): void {
    interval(1000)
      .pipe(
        switchMap(() => this.setUpCheckStreamHealth()),
        catchError((error) => {
          console.error('Error checking stream health', error);
          return of(null);
        }),
        takeUntil(this._destroy$)
      )
      .subscribe((result) => {
        if (result != null) {
          this.isStreamActive$.next(result);
        } else {
          this.isStreamActive$.next(false);
        }
      });
  }

  private setUpCheckStreamHealth(): Observable<boolean> {
    return this.streamIngestionService
      .checkStreamHealth()
      .pipe(catchError(() => of(false)));
  }

  private setUpStreamStoppingObservable(): void {
    this._stopStream$
      .pipe(
        switchMap(() => {
          console.log('Stopping Stream');

          return this.streamIngestionService.stopVideoStream();
        })
      )
      .subscribe(() => {
        this._getDrawnImage$.next();
      });
  }

  private setUpGetDrawnImage(): void {
    this._getDrawnImage$
      .pipe(
        switchMap(() => {
          return this.imageProcessingService.getDrawnImage();
        })
      )
      .subscribe((image) => {
        this.drawnImageUrl = URL.createObjectURL(image);
      });
  }
}
