import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable()
export class StreamIngestionService {
  private url: string = 'http://localhost:5000/video';

  constructor(private readonly _httpClient: HttpClient) {}

  public getVideoStream(): Observable<ArrayBuffer> {
    return this._httpClient.get(`${this.url}/video-feed`, {
      responseType: 'arraybuffer',
    });
  }

  public stopVideoStream(): Observable<void> {
    return this._httpClient.get<void>(`${this.url}/stop-video`);
  }
}
