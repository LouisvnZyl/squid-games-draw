import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable()
export class StreamIngestionService {
  private url: string = 'http://localhost:5000/video/video_feed';

  constructor(private readonly _httpClient: HttpClient) {}

  public getVideoStream(): Observable<ArrayBuffer> {
    return this._httpClient.get('http://localhost:5000/video/video_feed', {
      responseType: 'arraybuffer',
    });
  }
}
