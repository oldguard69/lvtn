import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.scss']
})
export class UploadFileComponent implements OnInit {
  fileToUpload!: File;
  constructor(
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
  }

  handleFileInput(target: any) {
    const file = target.files.item(0);
    this.fileToUpload = file as File;
    console.log(target.files)
  }

  uploadFile() {
    this.apiService.uploadFile(this.fileToUpload).subscribe(data => {
      console.log('File has been upload')
      }, error => {
        console.log(error);
      });
  }

}
