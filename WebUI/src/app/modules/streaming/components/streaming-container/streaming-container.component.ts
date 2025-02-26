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
  take,
  takeUntil,
} from 'rxjs';

@Component({
  templateUrl: './streaming-container.component.html',
  providers: [StreamIngestionService],
  standalone: true,
})
export class StreamingContainer implements OnDestroy {
  streamUrl: string = 'http://localhost:5000/video/video-feed';
  videoElement: HTMLImageElement | null = null;

  public readonly isStreamActive$ = new BehaviorSubject<boolean>(false);

  private _stopStream$ = new Subject<void>();
  private readonly _destroy$ = new Subject<void>();

  constructor(private readonly streamIngestionService: StreamIngestionService) {
    this.setUpStreamStoppingObservable();
    this.setUpStreamEvaluation();
  }

  public ngOnDestroy(): void {
    this._destroy$.next();
    this._destroy$.complete();
  }

  public onStopVideo(): void {
    this._stopStream$.next();
  }

  private setUpStreamEvaluation(): void {
    interval(5000)
      .pipe(
        switchMap(() => this.setUpCheckStreamHealth()),
        catchError((error) => {
          console.error('Error checking stream health', error);
          return of(null);
        }),
        takeUntil(this._destroy$)
      )
      .subscribe((result) => {
        if (!result) {
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
      .subscribe();
  }
}
