import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable()
export class ImageProcessingService {
  private url: string = 'http://localhost:5000/image-processing';

  constructor(private readonly _httpClient: HttpClient) {}

  public getDrawnImage(): Observable<Blob> {
    return this._httpClient.get<Blob>(`${this.url}/drawn-image`, {
      responseType: 'blob' as 'json', // Tells Angular to expect a blob
    });
  }
}
