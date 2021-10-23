export interface SuspiciousStatItem {
    src_file: string;
    paragraph_length: number;
    src_start_index: number;
    susp_insert_index: number;
    colorClass: string;
    srcIndexRange: Set<number>;
    suspIndexRange: Set<number>;
}

export interface HighligthObject {
    indexRange: Set<number>;
    colorClass: string;
}

interface Test {
    [key: string]: SuspiciousStatItem
}