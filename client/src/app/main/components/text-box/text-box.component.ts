import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  Input,
} from '@angular/core';
import {
  SuspiciousStatItem,
  HighligthObject,
} from '../../interface/susp-stat.interface';

@Component({
  selector: 'app-text-box',
  templateUrl: './text-box.component.html',
  styleUrls: ['./text-box.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TextBoxComponent implements OnInit {
  @Input() sentences!: string[];
  @Input() fileType: 'susp' | 'src' = 'susp';
  @Input() fileStat!: SuspiciousStatItem[];
  @Input() srcFileName!: string | null;
  highlight!: HighligthObject[];

  constructor() {}

  ngOnInit(): void {
    if (this.fileType === 'src') {
      this.highlight = this.fileStat
        .filter((item) => item.srcFile === this.srcFileName)
        .map((item) => ({
          indexRange: item.srcIndexRange,
          colorClass: item.colorClass,
        }));
    } else {
      this.highlight = this.fileStat.map((item) => ({
        indexRange: item.suspIndexRange,
        colorClass: item.colorClass,
      }));
      console.log(this.highlight)
    }
  }

  getClassColor(i: number): string {
    for (let index = 0; index < this.highlight.length; index++) {
      if (this.highlight[index].indexRange.has(i)) {
        return this.highlight[index].colorClass;
      }
    }
    return 'no-color';
  }
}
