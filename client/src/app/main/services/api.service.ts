import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { SuspiciousStatItem } from '../interface/susp-stat.interface';
import { SuspiciousDoc } from '../interface/susp-doc';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(
    private http: HttpClient,
    @Inject('API_URL') private api_url: string
  ) {}

  fetchStatOfSuspiciousFile(
    filename: string
  ): Observable<SuspiciousStatItem[]> {
    return this.http
      .get<SuspiciousStatItem[]>(
        `${this.api_url}/suspicious-stats/${filename}.json`
      )
      .pipe(
        map((res) =>{

          const t = res.map((item, index) => ({
            ...item,
            colorClass: `color-${index}`,
            srcIndexRange: new Set(
              this.range(item.paragraph_length, item.src_start_index)
            ),
            suspIndexRange: new Set(
              this.range(item.paragraph_length, item.susp_insert_index)
            ),
          })

        )
          console.log(t)
          return t;
        })
      );
  }

  fetchSourceFileSentences(filename: string): Observable<string[]> {
    return this.http
      .get<string[]>(`${this.api_url}/source-doc-sentences/${filename}`)
      .pipe(map((res: any) => res['sentences']));
  }

  fetchSuspiciousFileSentences(filename: string): Observable<string[]> {
    return this.http
      .get(`${this.api_url}/suspicious-doc-sentences/${filename}`)
      .pipe(map((res: any) => res['sentences']));
  }

  range(size: number, startAt: number = 0): ReadonlyArray<number> {
    return [...Array(size).keys()].map((i) => i + startAt);
  }

  uploadFile(fileToUpload: File) {
    const formData: FormData = new FormData();
    formData.append('file', fileToUpload, fileToUpload.name);
    console.log(formData);
    return this.http.post(`${this.api_url}/upload-file`, formData).pipe(
      map((res: any) => {
        return res['result'];
      })
    );
  }

  fetchSuspiciousDocs(): Observable<SuspiciousDoc[]> {
    return this.http
      .get(`${this.api_url}/suspicious-docs`)
      .pipe(map((res: any) => res.result));
  }

  fetchSuspiciousDocDetail(doc_id: number): Observable<SuspiciousDoc> {
    return this.http
      .get(`${this.api_url}/suspicious-docs/${doc_id}`)
      .pipe(map((res: any) => res.result));
  }
}
