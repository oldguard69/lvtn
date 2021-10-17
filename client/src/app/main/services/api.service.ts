import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { SuspiciousStatItem } from '../interface/susp-stat.interface';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(
    private http: HttpClient,
    @Inject('API_URL') private api_url: string
  ) {}

  fetchSourceFileSentences(filename: string): Observable<string[]> {
    return this.http
      .get<string[]>(`${this.api_url}/source-doc/${filename}`)
      .pipe(map((res: any) => res['sentences']));
  }

  fetchSuspiciousFileSentences(filename: string): Observable<string[]> {
    return this.http
      .get(`${this.api_url}/suspicious-doc/${filename}`)
      .pipe(map((res: any) => res['sentences']));
  }

  fetchStatOfSuspiciousFile(
    filename: string
  ): Observable<SuspiciousStatItem[]> {
    return this.http
      .get<SuspiciousStatItem[]>(`${this.api_url}/suspicious-stat/${filename.slice(0, -4)}.json`)
      .pipe(
        map((res) =>
          res.map((item, index) => ({
            ...item,
            colorClass: `color-${index}`,
            srcIndexRange: new Set(
              this.range(item.paragraphLength, item.srcIndex)
            ),
            suspIndexRange: new Set(
              this.range(item.paragraphLength, item.suspIndex)
            ),
          }))
        )
      );
  }

  range(size: number, startAt: number = 0): ReadonlyArray<number> {
    return [...Array(size).keys()].map((i) => i + startAt);
  }

  uploadFile(fileToUpload: File) {
    const endpoint = 'your-destination-url';
    const formData: FormData = new FormData();
    formData.append('file', fileToUpload, fileToUpload.name);
    console.log(formData);
    return this.http
      .post(`${this.api_url}/upload-file`, formData).pipe(
        map(() => { return true; }),
      )
  }
}
