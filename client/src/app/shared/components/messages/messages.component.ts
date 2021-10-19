import { Component, Input } from '@angular/core';
import { ResponseMessage } from 'src/app/authentication/services/auth.service';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.scss']
})
export class MessagesComponent {
  @Input() messages?: ResponseMessage[];

}
